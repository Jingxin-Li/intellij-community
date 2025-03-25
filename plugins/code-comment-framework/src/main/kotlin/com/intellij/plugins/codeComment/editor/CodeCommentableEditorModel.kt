package com.intellij.plugins.codeComment.editor

import com.intellij.diff.util.LineRange
import com.intellij.openapi.util.Key

interface CodeCommentableEditorModel {
  fun canCreateComment(lineIdx: Int): Boolean
  
  fun requestNewComment(lineIdx: Int)
  
  fun cancelNewComment(lineIdx: Int)
  
  interface WithMultilineComments : CodeCommentableEditorModel {
    fun canCreateComment(lineRange: LineRange): Boolean
    
    fun requestNewComment(lineRange: LineRange)
  }
  
  companion object {
    val KEY: Key<CodeCommentEditorGutterControlsModel> = Key.create("CodeCommentableEditorModel")
  }
}
