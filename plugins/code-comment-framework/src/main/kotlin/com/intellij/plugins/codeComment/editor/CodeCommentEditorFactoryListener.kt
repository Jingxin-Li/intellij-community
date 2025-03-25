package com.intellij.plugins.codeComment.editor

import com.intellij.diff.util.LineRange
import com.intellij.openapi.editor.Editor
import com.intellij.openapi.editor.EditorFactory
import com.intellij.openapi.editor.EditorKind
import com.intellij.openapi.editor.event.EditorFactoryEvent
import com.intellij.openapi.editor.event.EditorFactoryListener
import com.intellij.openapi.editor.ex.EditorEx
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectManager
import com.intellij.plugins.codeComment.CodeCommentManager
import com.intellij.plugins.codeComment.model.CodeComment
import com.intellij.plugins.codeComment.ui.CodeCommentComponent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch

class CodeCommentEditorFactoryListener : EditorFactoryListener {
  
  override fun editorCreated(event: EditorFactoryEvent) {
    val editor = event.editor
    if (editor.editorKind != EditorKind.MAIN_EDITOR || editor !is EditorEx) {
      return
    }
    
    val document = editor.document
    val file = FileDocumentManager.getInstance().getFile(document) ?: return
    val project = guessProject(editor) ?: return
    
    val commentManager = CodeCommentManager.getInstance(project)
    val comments = commentManager.getCommentsForFile(file)
    
    if (comments.isEmpty()) {
      return
    }
    
    val controlsModel = createEditorControlsModel(editor, comments)
    editor.putUserData(CodeCommentableEditorModel.KEY, controlsModel)
    
    // As a demonstration, if we have comments in the file, show them
    val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    scope.launch {
      setupCommentsForEditor(editor, comments)
    }
  }
  
  private fun createEditorControlsModel(editor: EditorEx, comments: List<CodeComment>): CodeCommentEditorGutterControlsModel {
    val commentLines = comments.flatMap { comment -> 
      (comment.lineRange.start..comment.lineRange.end).toList() 
    }.toSet()
    
    val state = MutableStateFlow(
      CodeCommentEditorGutterControlsModel.ControlsState(
        linesWithComments = commentLines,
        linesWithNewComments = emptySet(),
        commentablePredicate = { true }
      )
    )
    
    return object : CodeCommentEditorGutterControlsModel {
      override val gutterControlsState = state
      
      override fun requestNewComment(lineIdx: Int) {
        // In a real implementation, this would show UI for creating a comment
      }
      
      override fun cancelNewComment(lineIdx: Int) {
        // In a real implementation, this would cancel comment creation
      }
      
      override fun toggleComments(lineIdx: Int) {
        // In a real implementation, this would show/hide comments
      }
    }
  }
  
  private fun setupCommentsForEditor(editor: EditorEx, comments: List<CodeComment>) {
    for (comment in comments) {
      val component = CodeCommentComponent(comment)
      
      // For demonstration purposes, insert the comment component after the last line in the range
      editor.inlayModel.addBlockElement(
        editor.document.getLineEndOffset(comment.lineRange.end),
        true, true, 0, component
      )
    }
  }
  
  private fun guessProject(editor: Editor): Project? {
    // Try to find a project for this editor
    return ProjectManager.getInstance().openProjects.firstOrNull()
  }
}
