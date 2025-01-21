package com.example.ducky;

import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.openapi.vfs.VirtualFileManager;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vcs.changes.ignore.cache.PatternCache;
import com.intellij.openapi.vcs.changes.ignore.lang.IgnoreFileType;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public final class DuckyFileIndexManager {
    private static final Logger LOG = Logger.getInstance(DuckyFileIndexManager.class);
    
    private final Project project;
    private final Set<String> ignoredPatterns;
    
    public DuckyFileIndexManager(@NotNull Project project) {
        this.project = project;
        this.ignoredPatterns = new HashSet<>();
        loadGitIgnorePatterns();
    }
    
    private void loadGitIgnorePatterns() {
        VirtualFile projectDir = project.getBaseDir();
        if (projectDir == null) {
            LOG.warn("Project base directory is null");
            return;
        }
        
        VirtualFile gitignoreFile = projectDir.findChild(".gitignore");
        if (gitignoreFile == null) {
            LOG.info("No .gitignore file found in project root");
            // Add default patterns
            ignoredPatterns.addAll(Arrays.asList(
                ".git/", "node_modules/", "build/", "dist/",
                "*.class", "*.log", "*.iml", ".idea/"
            ));
            return;
        }
        
        try {
            String content = new String(gitignoreFile.contentsToByteArray());
            for (String line : content.split("\n")) {
                line = line.trim();
                if (!line.isEmpty() && !line.startsWith("#")) {
                    ignoredPatterns.add(line);
                }
            }
        } catch (IOException e) {
            LOG.error("Failed to read .gitignore file", e);
        }
    }
    
    private boolean isIgnored(String path) {
        for (String pattern : ignoredPatterns) {
            if (PatternCache.INSTANCE.createPattern(pattern).matcher(path).matches()) {
                return true;
            }
        }
        return false;
    }
    
    public List<FileInfo> indexProjectFiles() {
        List<FileInfo> fileInfos = new ArrayList<>();
        VirtualFile projectDir = project.getBaseDir();
        
        if (projectDir == null) {
            LOG.error("Project base directory is null");
            return fileInfos;
        }
        
        indexDirectory(projectDir, fileInfos);
        return fileInfos;
    }
    
    private void indexDirectory(VirtualFile dir, List<FileInfo> fileInfos) {
        VirtualFile[] children = dir.getChildren();
        String basePath = project.getBasePath();
        if (basePath == null) {
            LOG.error("Project base path is null");
            return;
        }
        
        for (VirtualFile child : children) {
            String relativePath = child.getPath().substring(basePath.length() + 1);
            
            if (isIgnored(relativePath)) {
                continue;
            }
            
            if (child.isDirectory()) {
                indexDirectory(child, fileInfos);
            } else {
                fileInfos.add(new FileInfo(
                    relativePath,
                    child.getTimeStamp(),
                    child.getLength()
                ));
            }
        }
    }
    
    public static class FileInfo {
        private final String path;
        private final long lastModified;
        private final long size;
        
        public FileInfo(String path, long lastModified, long size) {
            this.path = path;
            this.lastModified = lastModified;
            this.size = size;
        }
        
        public String getPath() { return path; }
        public long getLastModified() { return lastModified; }
        public long getSize() { return size; }
    }
}
