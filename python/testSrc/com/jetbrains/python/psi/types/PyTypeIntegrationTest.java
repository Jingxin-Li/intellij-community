package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyTypeIntegrationTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Type checker and union type integration
    public void testTypeCheckerWithUnion() {
        doTest("Union[str, int]",
               """
               from typing import Union
               def process(x: Union[str, int]) -> Union[str, int]:
                   if isinstance(x, str):
                       expr = x.upper()
                   else:
                       expr = x + 1
                   return expr
               """);
    }

    // Collection type with type parameter mapping
    public void testCollectionWithTypeParams() {
        doTest("List[Dict[K, V]]",
               """
               from typing import TypeVar, List, Dict
               K = TypeVar('K')
               V = TypeVar('V')
               def transform(d: Dict[K, V]) -> List[Dict[K, V]]:
                   expr = [d]
                   return expr
               """);
    }

    // Function type with structural type
    public void testFunctionWithStructural() {
        doTest("Callable[[Any], Any]",
               """
               from typing import Protocol, Callable, Any
               class Processor(Protocol):
                   def process(self, x: Any) -> Any: ...
               def wrap_processor(p: Processor) -> Callable[[Any], Any]:
                   expr = p.process
                   return expr
               """);
    }

    // Generic class with union type
    public void testGenericWithUnion() {
        doTest("Container[Union[str, int]]",
               """
               from typing import Generic, TypeVar, Union, List
               T = TypeVar('T')
               class Container(Generic[T]):
                   def __init__(self, value: T):
                       self.value = value
               def create(x: Union[str, int]) -> Container[Union[str, int]]:
                   expr = Container(x)
                   return expr
               """);
    }

    // Protocol with collection type
    public void testProtocolWithCollection() {
        doTest("List[Sized]",
               """
               from typing import Protocol, List
               class Sized(Protocol):
                   def __len__(self) -> int: ...
               def collect_sized(items: List[Sized]) -> List[Sized]:
                   expr = items
                   return expr
               """);
    }

    // Type parameter with structural type
    public void testTypeVarWithStructural() {
        doTest("T",
               """
               from typing import TypeVar, Protocol
               class Comparable(Protocol):
                   def __lt__(self, other: Any) -> bool: ...
               T = TypeVar('T', bound=Comparable)
               def min_value(x: T, y: T) -> T:
                   expr = x if x < y else y
                   return expr
               """);
    }

    // Function type with collection and union
    public void testFunctionWithCollectionAndUnion() {
        doTest("Callable[[List[Union[str, int]]], Dict[str, List[int]]]",
               """
               from typing import Callable, List, Dict, Union
               def create_processor() -> Callable[[List[Union[str, int]]], Dict[str, List[int]]]:
                   def process(items: List[Union[str, int]]) -> Dict[str, List[int]]:
                       return {"nums": [int(x) for x in items if isinstance(x, (str, int))]}
                   expr = process
                   return expr
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
