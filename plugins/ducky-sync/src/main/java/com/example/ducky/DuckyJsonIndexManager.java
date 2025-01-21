package com.example.ducky;

import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

public final class DuckyJsonIndexManager {
    private static final Logger LOG = Logger.getInstance(DuckyJsonIndexManager.class);
    private static final String INDEX_DIR = System.getProperty("user.home") + "/.code_index";
    private final Project project;
    
    public DuckyJsonIndexManager(@NotNull Project project) {
        this.project = project;
    }
    
    public void writeIndex(@NotNull String hardwareId, @NotNull List<DuckyFileIndexManager.FileInfo> files) {
        String projectPath = sanitizeProjectPath(project.getBasePath());
        if (projectPath == null) {
            LOG.error("Failed to get project base path");
            return;
        }
        
        try {
            // Create directory if it doesn't exist
            Files.createDirectories(Paths.get(INDEX_DIR));
            
            // Create index file path
            Path indexPath = Paths.get(INDEX_DIR, hardwareId + "_" + projectPath + ".json");
            
            // Create JSON structure manually
            StringBuilder json = new StringBuilder();
            json.append("{\n  \"files\": [\n");
            
            String fileEntries = files.stream()
                .map(file -> String.format("    {\n" +
                    "      \"path\": \"%s\",\n" +
                    "      \"lastModified\": %d,\n" +
                    "      \"size\": %d\n" +
                    "    }", 
                    escapeJson(file.getPath()), 
                    file.getLastModified(),
                    file.getSize()))
                .collect(Collectors.joining(",\n"));
            
            json.append(fileEntries)
                .append("\n  ]\n}");
            
            // Write JSON to file
            Files.writeString(indexPath, json.toString());
            
            LOG.info("Successfully wrote index file: " + indexPath);
        } catch (IOException e) {
            LOG.error("Failed to write index file", e);
        }
    }
    
    private String escapeJson(String input) {
        return input.replace("\\", "\\\\")
                   .replace("\"", "\\\"")
                   .replace("\b", "\\b")
                   .replace("\f", "\\f")
                   .replace("\n", "\\n")
                   .replace("\r", "\\r")
                   .replace("\t", "\\t");
    }
    
    private String sanitizeProjectPath(String path) {
        if (path == null) {
            return null;
        }
        // Replace characters that are not suitable for filenames
        return path.replaceAll("[^a-zA-Z0-9.-]", "_");
    }
}
