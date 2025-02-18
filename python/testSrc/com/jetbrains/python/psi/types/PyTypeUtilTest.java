package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyTypeUtilTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Type comparison tests
    public void testTypeComparison() {
        doTest("bool",
               """
               def test_func(x: int, y: int) -> bool:
                   expr = isinstance(x, type(y))
                   return expr
               """);
    }

    public void testSubtypeCheck() {
        doTest("bool",
               """
               class A:
                   pass
               class B(A):
                   pass
               def test_func(x: B) -> bool:
                   expr = isinstance(x, A)
                   return expr
               """);
    }

    // Type substitution tests
    public void testTypeSubstitution() {
        doTest("List[int]",
               """
               from typing import List, TypeVar
               T = TypeVar('T')
               def identity(x: List[T]) -> List[T]:
                   return x
               expr = identity([1, 2, 3])
               """);
    }

    public void testNestedTypeSubstitution() {
        doTest("Dict[str, List[int]]",
               """
               from typing import Dict, List, TypeVar
               T = TypeVar('T')
               def wrap_dict(x: T) -> Dict[str, List[T]]:
                   return {"items": [x]}
               expr = wrap_dict(42)
               """);
    }

    // Type unification tests
    public void testTypeUnification() {
        doTest("Union[str, int]",
               """
               from typing import Union
               def choose(condition: bool) -> Union[str, int]:
                   expr = "text" if condition else 42
                   return expr
               """);
    }

    public void testTypeUnificationWithSubtypes() {
        doTest("A",
               """
               class A:
                   pass
               class B(A):
                   pass
               class C(A):
                   pass
               def choose(condition: bool) -> A:
                   expr = B() if condition else C()
                   return expr
               """);
    }

    // Edge cases
    public void testNoneType() {
        doTest("None",
               """
               def test_func() -> None:
                   expr = None
                   return expr
               """);
    }

    public void testAnyType() {
        doTest("Any",
               """
               from typing import Any
               def test_func(x: Any) -> Any:
                   expr = x
                   return expr
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
