package com.intellij.plugins.codeComment.editor

import com.intellij.openapi.editor.Inlay
import com.intellij.openapi.editor.markup.GutterIconRenderer
import com.intellij.plugins.codeComment.model.CodeComment
import com.intellij.plugins.codeComment.ui.CodeCommentComponent
import javax.swing.JComponent

class CodeCommentInlayRenderer(
  private val comment: CodeComment,
  private val component: JComponent = CodeCommentComponent(comment)
) : ComponentInlayRenderer<JComponent>(component) {
  
  override fun calcGutterIconRenderer(inlay: Inlay<*>): GutterIconRenderer? {
    return CodeCommentGutterIconRenderer(comment.id)
  }
  
  override fun toString(): String = "CodeCommentInlayRenderer(comment=$comment)"
}
