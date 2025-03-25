package com.intellij.plugins.codeComment.settings

import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service

@Service
class CodeCommentSettings {
  var enableComments: Boolean = true
  var maxCommentWidth: Int = 400
  
  companion object {
    fun getInstance(): CodeCommentSettings = service()
  }
}
