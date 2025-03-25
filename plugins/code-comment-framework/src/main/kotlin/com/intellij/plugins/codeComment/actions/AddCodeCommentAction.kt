package com.intellij.plugins.codeComment.actions

import com.intellij.diff.util.LineRange
import com.intellij.openapi.actionSystem.ActionUpdateThread
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.editor.Editor
import com.intellij.openapi.editor.ex.EditorEx
import com.intellij.openapi.project.DumbAware
import com.intellij.openapi.ui.Messages
import com.intellij.plugins.codeComment.CodeCommentManager
import com.intellij.plugins.codeComment.editor.CodeCommentableEditorModel

class AddCodeCommentAction : AnAction(), DumbAware {
  
  override fun getActionUpdateThread(): ActionUpdateThread = ActionUpdateThread.EDT
  
  override fun update(e: AnActionEvent) {
    val editor = e.getData(CommonDataKeys.EDITOR) as? EditorEx
    val file = e.getData(CommonDataKeys.VIRTUAL_FILE)
    
    e.presentation.isEnabledAndVisible = editor != null && file != null
  }
  
  override fun actionPerformed(e: AnActionEvent) {
    val editor = e.getData(CommonDataKeys.EDITOR) as? EditorEx ?: return
    val project = e.getProject() ?: return
    val file = e.getData(CommonDataKeys.VIRTUAL_FILE) ?: return
    
    val selectionModel = editor.selectionModel
    if (!selectionModel.hasSelection()) {
      return
    }
    
    val startLine = editor.document.getLineNumber(selectionModel.selectionStart)
    val endLine = editor.document.getLineNumber(selectionModel.selectionEnd)
    val lineRange = LineRange(startLine, endLine)
    
    val text = Messages.showInputDialog(
      project,
      "Enter comment text:",
      "Add Code Comment",
      null
    ) ?: return
    
    val commentManager = CodeCommentManager.getInstance(project)
    val comment = commentManager.addComment(file, lineRange, text)
    
    // Example of adding a suggestion to the comment
    if (Messages.showYesNoDialog(
        project,
        "Do you want to add a sample code suggestion?",
        "Add Code Suggestion",
        "Yes", "No", null
      ) == Messages.YES) {
      
      val selectedText = editor.selectionModel.selectedText ?: ""
      val suggestedText = "// " + selectedText.replace("\n", "\n// ")
      
      commentManager.addSuggestion(file, comment, editor.document, lineRange, suggestedText)
    }
  }
}
