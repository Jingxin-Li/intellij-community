package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyCollectionTypeTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // List type tests
    public void testListType() {
        doTest("List[int]",
               """
               from typing import List
               def process_list(x: List[int]) -> List[int]:
                   expr = x
                   return x
               """);
    }

    public void testNestedListType() {
        doTest("List[List[str]]",
               """
               from typing import List
               def process_nested(x: List[List[str]]) -> List[List[str]]:
                   expr = x
                   return x
               """);
    }

    // Dict type tests
    public void testDictType() {
        doTest("Dict[str, int]",
               """
               from typing import Dict
               def process_dict(x: Dict[str, int]) -> Dict[str, int]:
                   expr = x
                   return x
               """);
    }

    public void testNestedDictType() {
        doTest("Dict[str, Dict[str, int]]",
               """
               from typing import Dict
               def process_nested(x: Dict[str, Dict[str, int]]):
                   expr = x
                   return x
               """);
    }

    // Set type tests
    public void testSetType() {
        doTest("Set[int]",
               """
               from typing import Set
               def process_set(x: Set[int]) -> Set[int]:
                   expr = x
                   return x
               """);
    }

    public void testFrozenSetType() {
        doTest("FrozenSet[str]",
               """
               from typing import FrozenSet
               def process_frozen(x: FrozenSet[str]) -> FrozenSet[str]:
                   expr = x
                   return x
               """);
    }

    // Collection with type vars
    public void testCollectionWithTypeVar() {
        doTest("List[T]",
               """
               from typing import TypeVar, List
               T = TypeVar('T')
               def process_generic(x: List[T]) -> List[T]:
                   expr = x
                   return x
               """);
    }

    public void testCollectionWithBoundedTypeVar() {
        doTest("List[str]",
               """
               from typing import TypeVar, List
               S = TypeVar('S', bound=str)
               def process_strings(x: List[S]) -> List[S]:
                   expr = x
                   return x
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
