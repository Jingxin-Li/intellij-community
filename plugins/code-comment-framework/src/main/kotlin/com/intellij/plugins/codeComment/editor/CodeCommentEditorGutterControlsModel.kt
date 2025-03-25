package com.intellij.plugins.codeComment.editor

import kotlinx.coroutines.flow.StateFlow

interface CodeCommentEditorGutterControlsModel {
  val gutterControlsState: StateFlow<ControlsState>
  
  fun requestNewComment(lineIdx: Int)
  
  fun cancelNewComment(lineIdx: Int)
  
  fun toggleComments(lineIdx: Int)
  
  data class ControlsState(
    val linesWithComments: Set<Int>,
    val linesWithNewComments: Set<Int>,
    val commentablePredicate: (Int) -> Boolean
  ) {
    fun isLineCommentable(line: Int): Boolean = commentablePredicate(line)
  }
}
