package com.intellij.plugins.codeComment.sample

import com.intellij.diff.util.LineRange
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.editor.Document
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.startup.StartupActivity
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.plugins.codeComment.CodeCommentManager
import com.intellij.plugins.codeComment.model.CodeComment

class SampleCommentGenerator : StartupActivity.DumbAware {
  override fun runActivity(project: Project) {
    val currentFile = guessCurrentFile(project) ?: return
    val document = getDocumentFor(currentFile) ?: return
    
    // Create a demonstration code comment on lines 10-20 (if the file has that many lines)
    if (document.lineCount > 20) {
      ApplicationManager.getApplication().invokeLater {
        generateSampleComment(project, currentFile, document)
      }
    }
  }
  
  private fun generateSampleComment(project: Project, file: VirtualFile, document: Document) {
    val commentManager = CodeCommentManager.getInstance(project)
    
    // Create a comment spanning lines 10-20
    val lineRange = LineRange(10, 20)
    val comment = commentManager.addComment(
      file, 
      lineRange,
      "This is a sample comment attached to lines 10-20 of this file."
    )
    
    // Extract the original text from these lines
    val startOffset = document.getLineStartOffset(lineRange.start)
    val endOffset = document.getLineEndOffset(lineRange.end)
    val originalText = document.getText(startOffset..endOffset)
    
    // Create a code suggestion with some modifications to the original text
    val lines = originalText.split("\n")
    val modifiedLines = lines.mapIndexed { index, line ->
      if (index == 0) "// MODIFIED: $line"
      else if (index % 2 == 0) "// SUGGESTED CHANGE: $line"
      else line
    }
    
    val suggestedText = modifiedLines.joinToString("\n")
    
    // Add the suggestion to the comment
    commentManager.addSuggestion(file, comment, document, lineRange, suggestedText)
  }
  
  private fun guessCurrentFile(project: Project): VirtualFile? {
    val fileEditorManager = FileEditorManager.getInstance(project)
    return fileEditorManager.selectedFiles.firstOrNull()
  }
  
  private fun getDocumentFor(file: VirtualFile): Document? {
    return FileDocumentManager.getInstance().getDocument(file)
  }
}
