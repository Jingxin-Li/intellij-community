package com.example.ducky;

import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;
import java.util.List;

public final class DuckyMockCompletionService {
    private static final Logger LOG = Logger.getInstance(DuckyMockCompletionService.class);
    private final Project project;

    public DuckyMockCompletionService(@NotNull Project project) {
        this.project = project;
    }

    public List<String> getCodeCompletionSuggestions(@NotNull String context, @NotNull String hardwareId) {
        LOG.info("Mock: Requesting code completion suggestions");
        LOG.info("Mock: Using hardware ID: " + hardwareId);
        LOG.info("Mock: Context length: " + context.length() + " characters");

        // Mock response with placeholder suggestions
        return Arrays.asList(
            "// Mock completion suggestion 1",
            "System.out.println(\"Hello World\");",
            "// Mock completion suggestion 2",
            "List<String> items = new ArrayList<>();"
        );
    }

    public List<String> getProgrammingTaskSuggestions(@NotNull String taskDescription, @NotNull String hardwareId) {
        LOG.info("Mock: Processing programming task request");
        LOG.info("Mock: Using hardware ID: " + hardwareId);
        LOG.info("Mock: Task description length: " + taskDescription.length() + " characters");

        // Mock response with placeholder task-related code
        return Arrays.asList(
            "// Mock implementation for: " + taskDescription,
            "public class TaskSolution {",
            "    public void solve() {",
            "        // TODO: Implement task solution",
            "        System.out.println(\"Mock solution\");",
            "    }",
            "}"
        );
    }

    public String getRelevantContext(@NotNull String query, @NotNull String hardwareId) {
        LOG.info("Mock: Fetching relevant context for query");
        LOG.info("Mock: Using hardware ID: " + hardwareId);

        // Mock response with placeholder context
        return "// Mock relevant context\n" +
               "// Related code from project files would appear here\n" +
               "public class MockContext {\n" +
               "    // Relevant methods and implementations\n" +
               "}";
    }
}
