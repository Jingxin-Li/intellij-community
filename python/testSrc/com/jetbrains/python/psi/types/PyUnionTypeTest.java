package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyUnionTypeTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Basic union type tests
    public void testBasicUnion() {
        doTest("Union[str, int]",
               """
               from typing import Union
               def test_func(x: Union[str, int]) -> Union[str, int]:
                   expr = x
                   return expr
               """);
    }

    public void testUnionWithNone() {
        doTest("Optional[str]",
               """
               from typing import Optional
               def test_func(x: Optional[str]) -> Optional[str]:
                   expr = x
                   return expr
               """);
    }

    // Union type inference tests
    public void testUnionInference() {
        doTest("Union[str, int]",
               """
               def test_func(condition: bool):
                   expr = "hello" if condition else 42
                   return expr
               """);
    }

    public void testNestedUnionInference() {
        doTest("Union[str, int, float]",
               """
               from typing import Union
               def test_func(x: Union[str, int], y: Union[int, float]):
                   expr = x if isinstance(x, str) else y
                   return expr
               """);
    }

    // Union type simplification tests
    public void testUnionSimplification() {
        doTest("int",
               """
               from typing import Union
               def test_func(x: Union[int, int]) -> int:
                   expr = x
                   return expr
               """);
    }

    public void testUnionWithSubtypes() {
        doTest("A",
               """
               class A: pass
               class B(A): pass
               def test_func(x: Union[A, B]) -> A:
                   expr = x
                   return expr
               """);
    }

    // Union type with collections
    public void testUnionWithCollections() {
        doTest("Union[List[int], Dict[str, int]]",
               """
               from typing import Union, List, Dict
               def test_func(x: Union[List[int], Dict[str, int]]):
                   expr = x
                   return expr
               """);
    }

    public void testUnionWithGenerics() {
        doTest("Union[List[T], None]",
               """
               from typing import TypeVar, Union, List, Optional
               T = TypeVar('T')
               def test_func(x: Optional[List[T]]) -> Optional[List[T]]:
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
