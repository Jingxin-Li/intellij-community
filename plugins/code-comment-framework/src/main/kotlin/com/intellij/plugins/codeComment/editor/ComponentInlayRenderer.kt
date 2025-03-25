package com.intellij.plugins.codeComment.editor

import com.intellij.openapi.editor.EditorCustomElementRenderer
import com.intellij.openapi.editor.Inlay
import com.intellij.openapi.editor.markup.GutterIconRenderer
import javax.swing.JComponent

/**
 * Base class for rendering components in editor inlays
 */
abstract class ComponentInlayRenderer<T : JComponent>(
  protected val component: T
) : EditorCustomElementRenderer {
  
  enum class ComponentInlayAlignment {
    FIT_VIEWPORT_WIDTH,
    CONTENT_WIDTH
  }
  
  open fun calcGutterIconRenderer(inlay: Inlay<*>): GutterIconRenderer? = null
  
  override fun calcWidthInPixels(inlay: Inlay<*>): Int {
    return component.preferredSize.width
  }
  
  override fun calcHeightInPixels(inlay: Inlay<*>): Int {
    return component.preferredSize.height
  }
  
  override fun paint(inlay: Inlay<*>, g: java.awt.Graphics, targetRegion: java.awt.Rectangle, textAttributes: com.intellij.openapi.editor.markup.TextAttributes) {
    component.setBounds(targetRegion)
    component.paint(g)
  }
}
