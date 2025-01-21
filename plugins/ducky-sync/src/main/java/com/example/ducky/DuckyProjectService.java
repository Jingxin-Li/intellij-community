package com.example.ducky;

import com.intellij.openapi.components.Service;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

@Service(Service.Level.PROJECT)
public final class DuckyProjectService {
    private static final Logger LOG = Logger.getInstance(DuckyProjectService.class);
    private final @NotNull Project project;

    public DuckyProjectService(@NotNull Project project) {
        this.project = project;
    }

    public void initialize() {
        LOG.info("Initializing DuckyProjectService for project: " + project.getName());
        String hardwareId = DuckyHardwareIdManager.getHardwareId();
        LOG.info("Using hardware ID: " + hardwareId);
        // Further implementation will be added in subsequent steps
    }
}
