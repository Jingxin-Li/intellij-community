package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyFunctionTypeTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Basic function type tests
    public void testBasicFunctionType() {
        doTest("(x: int) -> str",
               """
               def test_func(x: int) -> str:
                   return str(x)
               expr = test_func
               """);
    }

    public void testFunctionWithMultipleParams() {
        doTest("(x: int, y: str) -> bool",
               """
               def test_func(x: int, y: str) -> bool:
                   return len(y) == x
               expr = test_func
               """);
    }

    // Function type with type vars
    public void testGenericFunctionType() {
        doTest("(x: T) -> T",
               """
               from typing import TypeVar
               T = TypeVar('T')
               def identity(x: T) -> T:
                   return x
               expr = identity
               """);
    }

    public void testGenericFunctionWithConstraints() {
        doTest("(x: Union[str, int]) -> Union[str, int]",
               """
               from typing import TypeVar, Union
               T = TypeVar('T', str, int)
               def process(x: T) -> T:
                   return x
               expr = process
               """);
    }

    // Function type with default values
    public void testFunctionWithDefaults() {
        doTest("(x: int, y: str = ...) -> str",
               """
               def test_func(x: int, y: str = "default") -> str:
                   return y * x
               expr = test_func
               """);
    }

    public void testFunctionWithOptionalParam() {
        doTest("(x: Optional[int]) -> Optional[str]",
               """
               from typing import Optional
               def test_func(x: Optional[int]) -> Optional[str]:
                   return str(x) if x is not None else None
               expr = test_func
               """);
    }

    // Function type with *args and **kwargs
    public void testFunctionWithVarArgs() {
        doTest("(*args: int) -> List[int]",
               """
               from typing import List
               def test_func(*args: int) -> List[int]:
                   return list(args)
               expr = test_func
               """);
    }

    public void testFunctionWithKwArgs() {
        doTest("(**kwargs: str) -> Dict[str, str]",
               """
               from typing import Dict
               def test_func(**kwargs: str) -> Dict[str, str]:
                   return kwargs
               expr = test_func
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
