package com.intellij.plugins.codeComment.ui

import com.intellij.openapi.actionSystem.ActionManager
import com.intellij.openapi.actionSystem.DefaultActionGroup
import com.intellij.openapi.ui.popup.JBPopupFactory
import com.intellij.plugins.codeComment.model.CodeComment
import com.intellij.ui.JBColor
import com.intellij.ui.components.JBLabel
import com.intellij.ui.components.JBPanel
import com.intellij.ui.components.JBScrollPane
import com.intellij.util.ui.JBUI
import java.awt.BorderLayout
import java.awt.Dimension
import javax.swing.JComponent
import javax.swing.JPanel
import javax.swing.border.CompoundBorder

class CodeCommentComponent(
  private val comment: CodeComment
) : JBPanel<CodeCommentComponent>(BorderLayout()) {
  
  init {
    isOpaque = false
    border = JBUI.Borders.empty(10)
    
    val header = JBPanel<JPanel>(BorderLayout()).apply {
      isOpaque = false
      border = JBUI.Borders.empty(0, 0, 8, 0)
      
      add(JBLabel("Comment").apply {
        font = font.deriveFont(font.style or java.awt.Font.BOLD)
      }, BorderLayout.WEST)
    }
    
    val content = JBPanel<JPanel>(BorderLayout()).apply {
      isOpaque = true
      background = JBColor.background()
      border = CompoundBorder(
        JBUI.Borders.customLine(JBColor.border(), 1), 
        JBUI.Borders.empty(8)
      )
      
      add(JBLabel(comment.text), BorderLayout.NORTH)
      
      if (comment.suggestions.isNotEmpty()) {
        val suggestionsPanel = JBPanel<JPanel>(BorderLayout()).apply {
          isOpaque = false
          border = JBUI.Borders.emptyTop(8)
          
          for (suggestion in comment.suggestions) {
            add(CodeSuggestionComponent(suggestion), BorderLayout.NORTH)
          }
        }
        
        add(suggestionsPanel, BorderLayout.CENTER)
      }
    }
    
    add(header, BorderLayout.NORTH)
    add(content, BorderLayout.CENTER)
  }
  
  override fun getPreferredSize(): Dimension {
    val size = super.getPreferredSize()
    return Dimension(size.width.coerceAtMost(400), size.height)
  }
}
