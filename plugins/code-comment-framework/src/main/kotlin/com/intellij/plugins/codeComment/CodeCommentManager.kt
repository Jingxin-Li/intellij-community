package com.intellij.plugins.codeComment

import com.intellij.diff.util.LineRange
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service
import com.intellij.openapi.editor.Document
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.plugins.codeComment.model.CodeComment
import com.intellij.plugins.codeComment.model.CodeSuggestion

@Service(Service.Level.PROJECT)
class CodeCommentManager(private val project: Project) {
  
  private val commentsByFile = mutableMapOf<String, MutableList<CodeComment>>()
  
  fun getCommentsForFile(file: VirtualFile): List<CodeComment> {
    return commentsByFile[file.path] ?: emptyList()
  }
  
  fun addComment(file: VirtualFile, lineRange: LineRange, text: String): CodeComment {
    val comment = CodeComment(
      lineRange = lineRange,
      text = text
    )
    
    val comments = commentsByFile.getOrPut(file.path) { mutableListOf() }
    comments.add(comment)
    
    return comment
  }
  
  fun addSuggestion(file: VirtualFile, comment: CodeComment, document: Document, range: LineRange, suggestedText: String): CodeSuggestion {
    val suggestion = CodeSuggestion.createFromLineRange(document, range, suggestedText)
    
    val updatedSuggestions = comment.suggestions + suggestion
    val updatedComment = comment.copy(suggestions = updatedSuggestions)
    
    val comments = commentsByFile[file.path]
    val index = comments?.indexOfFirst { it.id == comment.id } ?: -1
    
    if (index >= 0 && comments != null) {
      comments[index] = updatedComment
    }
    
    return suggestion
  }
  
  companion object {
    fun getInstance(project: Project): CodeCommentManager = project.service()
  }
}
