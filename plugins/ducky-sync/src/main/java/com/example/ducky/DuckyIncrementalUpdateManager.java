package com.example.ducky;

import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import com.intellij.util.Alarm;
import org.jetbrains.annotations.NotNull;

public final class DuckyIncrementalUpdateManager {
    private static final Logger LOG = Logger.getInstance(DuckyIncrementalUpdateManager.class);
    private static final int UPDATE_INTERVAL_MS = 60000; // 1 minute

    private final Project project;
    private final Alarm alarm;
    private final DuckyFileIndexManager fileIndexManager;
    private final DuckyJsonIndexManager jsonIndexManager;
    private final DuckyUploadManager uploadManager;
    private final String hardwareId;

    public DuckyIncrementalUpdateManager(@NotNull Project project, @NotNull String hardwareId) {
        this.project = project;
        this.hardwareId = hardwareId;
        this.alarm = new Alarm(Alarm.ThreadToUse.POOLED_THREAD, project);
        this.fileIndexManager = new DuckyFileIndexManager(project);
        this.jsonIndexManager = new DuckyJsonIndexManager(project);
        this.uploadManager = new DuckyUploadManager(project);
    }

    public void startIncrementalUpdates() {
        LOG.info("Starting incremental updates for project: " + project.getName());
        scheduleNextUpdate();
    }

    private void scheduleNextUpdate() {
        if (project.isDisposed()) {
            LOG.info("Project is disposed, stopping incremental updates");
            return;
        }

        alarm.addRequest(() -> {
            try {
                performIncrementalUpdate();
            } finally {
                scheduleNextUpdate(); // Schedule next update regardless of success/failure
            }
        }, UPDATE_INTERVAL_MS);
    }

    private void performIncrementalUpdate() {
        LOG.info("Performing incremental update");
        var files = fileIndexManager.indexProjectFiles();
        jsonIndexManager.writeIndex(hardwareId, files);
        uploadManager.compressAndUpload(files);
        LOG.info("Incremental update completed");
    }

    public void dispose() {
        alarm.dispose();
    }
}
