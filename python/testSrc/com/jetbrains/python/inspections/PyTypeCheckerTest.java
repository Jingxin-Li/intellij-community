package com.jetbrains.python.inspections;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import com.jetbrains.python.psi.types.TypeEvalContext;
import org.jetbrains.annotations.NotNull;

public class PyTypeCheckerTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Basic type checking tests
    public void testBasicTypeChecking() {
        doTest("str",
               """
               def test_func(x: str) -> str:
                   return x
               expr = test_func("hello")
               """);
    }

    public void testTypeCheckingWithUnion() {
        doTest("Union[str, int]",
               """
               from typing import Union
               def test_func(x: Union[str, int]) -> Union[str, int]:
                   return x
               expr = test_func("hello")
               """);
    }

    public void testTypeCheckingWithOptional() {
        doTest("Optional[str]",
               """
               from typing import Optional
               def test_func(x: Optional[str]) -> Optional[str]:
                   return x
               expr = test_func(None)
               """);
    }

    // Generic type tests
    public void testTypeCheckingWithTypeVar() {
        doTest("int",
               """
               from typing import TypeVar, List
               T = TypeVar('T')
               def identity(x: T) -> T:
                   return x
               expr = identity(42)
               """);
    }

    public void testTypeCheckingWithBoundedTypeVar() {
        doTest("str",
               """
               from typing import TypeVar
               S = TypeVar('S', bound=str)
               def process_str(x: S) -> S:
                   return x.upper()
               expr = process_str("hello")
               """);
    }

    // Collection type tests
    public void testTypeCheckingWithList() {
        doTest("List[int]",
               """
               from typing import List
               def sum_list(x: List[int]) -> List[int]:
                   return [i + 1 for i in x]
               expr = sum_list([1, 2, 3])
               """);
    }

    public void testTypeCheckingWithDict() {
        doTest("Dict[str, int]",
               """
               from typing import Dict
               def process_dict(x: Dict[str, int]) -> Dict[str, int]:
                   return {k: v + 1 for k, v in x.items()}
               expr = process_dict({"a": 1})
               """);
    }

    // Protocol type tests
    public void testTypeCheckingWithProtocol() {
        doTest("Any",
               """
               from typing import Protocol
               class Sized(Protocol):
                   def __len__(self) -> int: ...
               def get_size(x: Sized) -> int:
                   return len(x)
               expr = get_size([1, 2, 3])
               """);
    }

    // Literal type tests
    public void testTypeCheckingWithLiteral() {
        doTest("Literal['success', 'error']",
               """
               from typing import Literal
               def get_status(success: bool) -> Literal['success', 'error']:
                   return 'success' if success else 'error'
               expr = get_status(True)
               """);
    }

    // Type narrowing tests
    public void testTypeNarrowing() {
        doTest("str",
               """
               from typing import Union
               def process(x: Union[str, int]) -> str:
                   if isinstance(x, str):
                       expr = x
                   return "default"
               """);
    }

    // Error cases
    public void testTypeCheckingWithIncompatibleTypes() {
        doTest("Any",
               """
               def str_only(x: str) -> str:
                   return x
               expr = str_only(42)  # Type error, but should still infer return type
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
