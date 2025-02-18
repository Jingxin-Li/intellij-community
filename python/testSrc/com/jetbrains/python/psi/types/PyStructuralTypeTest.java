package com.jetbrains.python.psi.types;

import com.jetbrains.python.fixtures.PyTestCase;
import com.jetbrains.python.psi.LanguageLevel;
import com.jetbrains.python.psi.PyExpression;
import org.jetbrains.annotations.NotNull;

public class PyStructuralTypeTest extends PyTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    // Basic structural type tests
    public void testBasicStructuralType() {
        doTest("{foo}",
               """
               def test_func(x):
                   x.foo
                   expr = x
               """);
    }

    public void testMultipleAttributes() {
        doTest("{foo, bar}",
               """
               def test_func(x):
                   x.foo
                   x.bar
                   expr = x
               """);
    }

    // Method call tests
    public void testMethodCall() {
        doTest("{foo}",
               """
               def test_func(x):
                   x.foo()
                   expr = x
               """);
    }

    public void testMethodCallWithArgs() {
        doTest("{foo}",
               """
               def test_func(x):
                   x.foo(1, 2)
                   expr = x
               """);
    }

    // Duck typing tests
    public void testDuckTyping() {
        doTest("{__len__}",
               """
               def test_func(x):
                   len(x)
                   expr = x
               """);
    }

    public void testDuckTypingWithIteration() {
        doTest("{__iter__}",
               """
               def test_func(x):
                   for item in x:
                       pass
                   expr = x
               """);
    }

    // Protocol-like behavior
    public void testProtocolLikeBehavior() {
        doTest("{read, write}",
               """
               def test_func(x):
                   x.read()
                   x.write("data")
                   expr = x
               """);
    }

    public void testContextManagerProtocol() {
        doTest("{__enter__, __exit__}",
               """
               def test_func(x):
                   with x:
                       pass
                   expr = x
               """);
    }

    private void doTest(final String expectedType, final String text) {
        myFixture.configureByText(PythonFileType.INSTANCE, text);
        final PyExpression expr = myFixture.findElementByText("expr", PyExpression.class);
        assertType(expectedType, expr, TypeEvalContext.codeAnalysis(expr.getProject(), expr.getContainingFile()));
    }
}
