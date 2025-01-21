package com.example.ducky;

import com.intellij.openapi.diagnostic.Logger;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

public final class DuckyHardwareIdManager {
    private static final Logger LOG = Logger.getInstance(DuckyHardwareIdManager.class);
    private static final String HARDWARE_ID_DIR = System.getProperty("user.home") + "/.code_index";
    private static final String HARDWARE_ID_FILE = HARDWARE_ID_DIR + "/hardware_id.txt";
    private static String cachedHardwareId = null;

    private DuckyHardwareIdManager() {
        // Utility class, no instantiation
    }

    @NotNull
    public static synchronized String getHardwareId() {
        if (cachedHardwareId != null) {
            return cachedHardwareId;
        }

        try {
            Path dirPath = Paths.get(HARDWARE_ID_DIR);
            Path filePath = Paths.get(HARDWARE_ID_FILE);

            if (Files.exists(filePath)) {
                cachedHardwareId = Files.readString(filePath).trim();
                LOG.info("Retrieved existing hardware ID: " + cachedHardwareId);
                return cachedHardwareId;
            }

            // Generate new hardware ID
            cachedHardwareId = UUID.randomUUID().toString();
            LOG.info("Generated new hardware ID: " + cachedHardwareId);

            // Create directory if it doesn't exist
            Files.createDirectories(dirPath);
            
            // Save hardware ID to file
            Files.writeString(filePath, cachedHardwareId);
            
            return cachedHardwareId;
        } catch (IOException e) {
            LOG.error("Failed to manage hardware ID file", e);
            // Fallback to in-memory ID if file operations fail
            if (cachedHardwareId == null) {
                cachedHardwareId = UUID.randomUUID().toString();
                LOG.warn("Using in-memory hardware ID due to file operation failure: " + cachedHardwareId);
            }
            return cachedHardwareId;
        }
    }
}
