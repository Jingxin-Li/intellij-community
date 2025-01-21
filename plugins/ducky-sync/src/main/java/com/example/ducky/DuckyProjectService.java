package com.example.ducky;

import com.intellij.openapi.components.Service;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

import java.util.List;
import com.intellij.openapi.Disposable;

@Service(Service.Level.PROJECT)
public final class DuckyProjectService implements com.intellij.openapi.Disposable {
    private static final Logger LOG = Logger.getInstance(DuckyProjectService.class);
    private final @NotNull Project project;

    public DuckyProjectService(@NotNull Project project) {
        this.project = project;
    }

    private DuckyFileIndexManager fileIndexManager;
    private String hardwareId;
    private DuckyIncrementalUpdateManager incrementalUpdateManager;
    private DuckyMockCompletionService completionService;

    public void initialize() {
        LOG.info("Initializing DuckyProjectService for project: " + project.getName());
        
        // Initialize hardware ID
        hardwareId = DuckyHardwareIdManager.getHardwareId();
        LOG.info("Using hardware ID: " + hardwareId);
        
        // Initialize and run file indexing
        fileIndexManager = new DuckyFileIndexManager(project);
        List<DuckyFileIndexManager.FileInfo> files = fileIndexManager.indexProjectFiles();
        LOG.info("Indexed " + files.size() + " files in project");
        
        // Write index file
        DuckyJsonIndexManager jsonIndexManager = new DuckyJsonIndexManager(project);
        jsonIndexManager.writeIndex(hardwareId, files);
        
        // Compress and upload files
        DuckyUploadManager uploadManager = new DuckyUploadManager(project);
        uploadManager.compressAndUpload(files);
        
        // Start incremental updates
        incrementalUpdateManager = new DuckyIncrementalUpdateManager(project, hardwareId);
        incrementalUpdateManager.startIncrementalUpdates();

        // Initialize completion service
        completionService = new DuckyMockCompletionService(project);
        LOG.info("Mock completion service initialized");
    }

    public List<String> getCodeCompletionSuggestions(@NotNull String context) {
        return completionService.getCodeCompletionSuggestions(context, hardwareId);
    }

    public List<String> getProgrammingTaskSuggestions(@NotNull String taskDescription) {
        return completionService.getProgrammingTaskSuggestions(taskDescription, hardwareId);
    }

    public String getRelevantContext(@NotNull String query) {
        return completionService.getRelevantContext(query, hardwareId);
    }

    @Override
    public void dispose() {
        if (incrementalUpdateManager != null) {
            incrementalUpdateManager.dispose();
        }
    }
}
