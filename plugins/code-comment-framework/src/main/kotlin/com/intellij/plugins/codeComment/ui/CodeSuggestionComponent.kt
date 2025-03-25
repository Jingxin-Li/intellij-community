package com.intellij.plugins.codeComment.ui

import com.intellij.diff.comparison.ComparisonManager
import com.intellij.diff.comparison.ComparisonPolicy
import com.intellij.diff.fragments.LineFragment
import com.intellij.openapi.editor.colors.EditorColorsManager
import com.intellij.openapi.editor.markup.EffectType
import com.intellij.openapi.editor.markup.TextAttributes
import com.intellij.plugins.codeComment.model.CodeSuggestion
import com.intellij.ui.JBColor
import com.intellij.ui.components.JBLabel
import com.intellij.ui.components.JBPanel
import com.intellij.util.ui.JBUI
import com.intellij.util.ui.UIUtil
import java.awt.BorderLayout
import java.awt.Color
import java.awt.FlowLayout
import java.awt.Font
import javax.swing.JPanel
import javax.swing.border.Border

class CodeSuggestionComponent(
  private val suggestion: CodeSuggestion
) : JBPanel<CodeSuggestionComponent>(BorderLayout()) {
  
  private val deletedColor = JBColor.RED.darker()
  private val addedColor = JBColor.GREEN.darker()
  
  init {
    isOpaque = false
    border = JBUI.Borders.empty(10, 0, 0, 0)
    
    val header = JBPanel<JPanel>(BorderLayout()).apply {
      isOpaque = false
      border = JBUI.Borders.empty(0, 0, 5, 0)
      
      add(JBLabel("Suggested change:").apply {
        font = font.deriveFont(font.style or Font.BOLD)
      }, BorderLayout.WEST)
    }
    
    val diffPanel = createDiffPanel(suggestion)
    
    add(header, BorderLayout.NORTH)
    add(diffPanel, BorderLayout.CENTER)
    
    val actionsPanel = JPanel(FlowLayout(FlowLayout.RIGHT)).apply {
      isOpaque = false
      add(UIUtil.createSmallButton("Apply").apply {
        addActionListener {
          // Would implement the action to apply the suggestion
        }
      })
    }
    
    add(actionsPanel, BorderLayout.SOUTH)
  }
  
  private fun createDiffPanel(suggestion: CodeSuggestion): JPanel {
    val panel = JBPanel<JPanel>(BorderLayout()).apply {
      isOpaque = true
      background = UIUtil.getPanelBackground()
      border = JBUI.Borders.customLine(JBColor.border(), 1)
    }
    
    val originalLines = suggestion.originalText.split("\n")
    val suggestedLines = suggestion.suggestedText.split("\n")
    
    val fragments = ComparisonManager.getInstance().compareLines(
      originalLines, suggestedLines, ComparisonPolicy.DEFAULT, false
    )
    
    val diffContent = JBPanel<JPanel>().apply {
      isOpaque = true
      background = UIUtil.getPanelBackground()
      layout = BorderLayout()
      border = JBUI.Borders.empty(5)
      
      val diffLines = JBPanel<JPanel>().apply {
        isOpaque = false
        setLayout(null) // Using absolute positioning
        
        var y = 0
        val lineHeight = 20
        
        for (fragment in fragments) {
          // Show deleted lines
          for (i in fragment.startLine1 until fragment.endLine1) {
            add(createLineLabel("- " + originalLines[i], deletedColor).apply {
              setBounds(0, y, 400, lineHeight)
            })
            y += lineHeight
          }
          
          // Show added lines
          for (i in fragment.startLine2 until fragment.endLine2) {
            add(createLineLabel("+ " + suggestedLines[i], addedColor).apply {
              setBounds(0, y, 400, lineHeight)
            })
            y += lineHeight
          }
        }
        
        preferredSize = java.awt.Dimension(400, y)
      }
      
      add(diffLines, BorderLayout.CENTER)
    }
    
    panel.add(diffContent, BorderLayout.CENTER)
    return panel
  }
  
  private fun createLineLabel(text: String, color: Color): JBLabel {
    return JBLabel(text).apply {
      foreground = color
      font = EditorColorsManager.getInstance().globalScheme.getFont(UIUtil.getFontWithFallback("Monospaced", Font.PLAIN, 12))
    }
  }
}
