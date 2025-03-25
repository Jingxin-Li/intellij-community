package com.intellij.plugins.codeComment.model

import com.intellij.diff.util.LineRange
import com.intellij.openapi.editor.Document
import com.intellij.openapi.util.Key
import java.util.*

/**
 * Represents a comment attached to a code fragment
 */
data class CodeComment(
  val id: String = UUID.randomUUID().toString(),
  val lineRange: LineRange,
  val text: String,
  val suggestions: List<CodeSuggestion> = emptyList(),
  val timestamp: Long = System.currentTimeMillis()
)

/**
 * Represents a code suggestion within a comment
 */
data class CodeSuggestion(
  val id: String = UUID.randomUUID().toString(),
  val originalText: String,
  val suggestedText: String,
  val lineStartOffset: Int
) {
  companion object {
    fun createFromLineRange(document: Document, lineRange: LineRange, suggestedText: String): CodeSuggestion {
      val startOffset = document.getLineStartOffset(lineRange.start)
      val endOffset = document.getLineEndOffset(lineRange.end)
      val originalText = document.getText(startOffset..endOffset)
      
      return CodeSuggestion(
        originalText = originalText,
        suggestedText = suggestedText,
        lineStartOffset = startOffset
      )
    }
  }
}
