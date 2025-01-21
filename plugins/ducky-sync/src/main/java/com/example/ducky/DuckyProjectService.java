package com.example.ducky;

import com.intellij.openapi.components.Service;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

import java.util.List;

@Service(Service.Level.PROJECT)
public final class DuckyProjectService {
    private static final Logger LOG = Logger.getInstance(DuckyProjectService.class);
    private final @NotNull Project project;

    public DuckyProjectService(@NotNull Project project) {
        this.project = project;
    }

    private DuckyFileIndexManager fileIndexManager;
    private String hardwareId;

    public void initialize() {
        LOG.info("Initializing DuckyProjectService for project: " + project.getName());
        
        // Initialize hardware ID
        hardwareId = DuckyHardwareIdManager.getHardwareId();
        LOG.info("Using hardware ID: " + hardwareId);
        
        // Initialize and run file indexing
        fileIndexManager = new DuckyFileIndexManager(project);
        List<DuckyFileIndexManager.FileInfo> files = fileIndexManager.indexProjectFiles();
        LOG.info("Indexed " + files.size() + " files in project");
        
        // Further implementation will be added in subsequent steps
    }
}
