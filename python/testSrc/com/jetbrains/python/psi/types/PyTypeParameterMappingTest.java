package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyTypeParameterMappingTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Basic type parameter mapping tests
    public void testBasicTypeParameterMapping() {
        doTest("int",
               """
               from typing import TypeVar, List
               T = TypeVar('T')
               def identity(x: T) -> T:
                   expr = x
                   return x
               identity(42)
               """);
    }

    public void testTypeParameterInCollection() {
        doTest("List[str]",
               """
               from typing import TypeVar, List
               T = TypeVar('T')
               def process_list(x: List[T]) -> List[T]:
                   expr = x
                   return x
               process_list(["hello"])
               """);
    }

    // Multiple type parameters
    public void testMultipleTypeParameters() {
        doTest("Dict[str, int]",
               """
               from typing import TypeVar, Dict
               K = TypeVar('K')
               V = TypeVar('V')
               def map_values(d: Dict[K, V]) -> Dict[K, V]:
                   expr = d
                   return d
               map_values({"a": 1})
               """);
    }

    public void testNestedTypeParameters() {
        doTest("List[Dict[str, int]]",
               """
               from typing import TypeVar, List, Dict
               T = TypeVar('T')
               def wrap_list(x: T) -> List[T]:
                   return [x]
               expr = wrap_list({"a": 1})
               """);
    }

    // Bounded type parameters
    public void testBoundedTypeParameter() {
        doTest("str",
               """
               from typing import TypeVar
               S = TypeVar('S', bound=str)
               def process_str(x: S) -> S:
                   expr = x
                   return x
               process_str("hello")
               """);
    }

    public void testConstrainedTypeParameter() {
        doTest("Union[str, int]",
               """
               from typing import TypeVar, Union
               T = TypeVar('T', str, int)
               def process(x: T) -> T:
                   expr = x
                   return x
               process("hello")
               """);
    }

    // Generic class type parameters
    public void testGenericClassTypeParameter() {
        doTest("List[int]",
               """
               from typing import TypeVar, Generic, List
               T = TypeVar('T')
               class Container(Generic[T]):
                   def __init__(self, value: List[T]):
                       self.value = value
               c = Container([1, 2, 3])
               expr = c.value
               """);
    }

    public void testGenericClassInheritance() {
        doTest("List[str]",
               """
               from typing import TypeVar, Generic, List
               T = TypeVar('T')
               class BaseContainer(Generic[T]):
                   def __init__(self, value: List[T]):
                       self.value = value
               class StringContainer(BaseContainer[str]):
                   pass
               c = StringContainer(["a", "b"])
               expr = c.value
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
