package com.example.ducky;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.startup.StartupActivity;
import org.jetbrains.annotations.NotNull;

public class DuckyStartupActivity implements StartupActivity.DumbAware {
    @Override
    public void runActivity(@NotNull Project project) {
        // Initialize DuckyProjectService
        DuckyProjectService projectService = project.getService(DuckyProjectService.class);
        
        // Service will handle:
        // 1) Generate or retrieve hardwareId
        // 2) Perform initial indexing, ignoring .gitignore patterns
        // 3) Compress files & mock upload to Ducky
        // 4) Write index to ~/.code_index/{hardwareId}_{projectPath}.json
        projectService.initialize();
    }
}
