package com.intellij.plugins.codeComment.editor

import com.intellij.icons.AllIcons
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.editor.markup.GutterIconRenderer
import javax.swing.Icon

class CodeCommentGutterIconRenderer(private val commentId: String) : GutterIconRenderer() {
  
  override fun getIcon(): Icon = AllIcons.Gutter.JavadocRead
  
  override fun getTooltipText(): String = "Code comment"
  
  override fun equals(other: Any?): Boolean {
    if (this === other) return true
    if (javaClass != other?.javaClass) return false
    
    other as CodeCommentGutterIconRenderer
    
    return commentId == other.commentId
  }
  
  override fun hashCode(): Int {
    return commentId.hashCode()
  }
  
  override fun getClickAction(): AnAction? = null
}
