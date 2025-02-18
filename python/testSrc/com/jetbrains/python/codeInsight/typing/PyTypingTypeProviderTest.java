package com.jetbrains.python.codeInsight.typing;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import com.jetbrains.python.psi.types.TypeEvalContext;
import org.jetbrains.annotations.NotNull;

public class PyTypingTypeProviderTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // TypeVar tests
    public void testTypeVarBasic() {
        doTest("int",
               """
               from typing import TypeVar
               T = TypeVar('T')
               def identity(x: T) -> T:
                   return x
               expr = identity(42)
               """);
    }

    public void testTypeVarWithBound() {
        doTest("str",
               """
               from typing import TypeVar
               T = TypeVar('T', bound=str)
               def process_str(x: T) -> T:
                   return x.upper()
               expr = process_str("hello")
               """);
    }

    public void testTypeVarWithConstraints() {
        doTest("Union[str, int]",
               """
               from typing import TypeVar
               T = TypeVar('T', str, int)
               def process(x: T) -> T:
                   return x
               expr = process("hello")
               """);
    }

    // Protocol tests
    public void testProtocolBasic() {
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

    public void testProtocolWithTypeVar() {
        doTest("List[int]",
               """
               from typing import Protocol, TypeVar, List
               T = TypeVar('T')
               class Container(Protocol[T]):
                   def get(self) -> T: ...
               def extract(x: Container[T]) -> T:
                   return x.get()
               class IntList:
                   def get(self) -> List[int]:
                       return [1, 2, 3]
               expr = extract(IntList())
               """);
    }

    // Generic tests
    public void testGenericClass() {
        doTest("List[int]",
               """
               from typing import Generic, TypeVar, List
               T = TypeVar('T')
               class Stack(Generic[T]):
                   def __init__(self, items: List[T]):
                       self.items = items
                   def pop(self) -> T:
                       return self.items.pop()
               stack = Stack([1, 2, 3])
               expr = stack.items
               """);
    }

    public void testGenericWithMultipleTypeVars() {
        doTest("Dict[str, int]",
               """
               from typing import Generic, TypeVar, Dict
               K = TypeVar('K')
               V = TypeVar('V')
               class Cache(Generic[K, V]):
                   def __init__(self, data: Dict[K, V]):
                       self.data = data
               cache = Cache({'a': 1, 'b': 2})
               expr = cache.data
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
