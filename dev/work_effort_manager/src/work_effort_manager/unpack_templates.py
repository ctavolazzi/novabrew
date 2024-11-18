#!/usr/bin/env python3

import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TemplateManager:
    """Manages creation and storage of templates"""
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.script_dir, "static", "templates")

    def create_templates(self) -> bool:
        """Creates the templates directory and template files."""
        try:
            os.makedirs(self.templates_dir, exist_ok=True)

            # Create each template
            templates = {
                "work_effort.md": self._get_work_effort_template(),
                "_router.md": self._get_router_template(),
                "chat.md": self._get_chat_template()
            }

            for filename, content in templates.items():
                filepath = os.path.join(self.templates_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
                logger.info(f"Created template: {filename}")

            self._create_readme()
            logger.info(f"\nTemplates created in: {self.templates_dir}")
            return True

        except Exception as e:
            logger.error(f"Error creating templates: {str(e)}")
            return False

    def _get_work_effort_template(self) -> str:
        return """---
title: "{{we_id}}"
created: {{date}}
status: in-progress
type: documentation
aliases:
  - {{we_id}} Implementation
tags:
  - work-effort
  - technical-requirements
  - system-design
  - documentation
related:
  - "[[Work Efforts Management]]"
  - "[[Technical Documentation]]"
  - "[[Implementation Guidelines]]"
parent-effort: null
child-efforts: []
related-efforts: []
chat-router: "[[{{we_id}}/_router-{{we_id}}]]"
recent-chats: []
---

# {{we_id}}

## Initial Setup

> [!question] Initial Requirements
> **Preview:** [Brief description]
>
> > [!abstract]- Full Content (Click to expand)
> > ```markdown
> > [Detailed content]
> > ```

## Technical Requirements Development

### {{we_id}} - Iteration 1
[Initial iteration content]

## Overview
[Add work effort overview here]

## Objectives
- [ ] First objective
- [ ] Second objective

## Related Pages
- [[Work Efforts Management]]
- [[Technical Documentation]]
- [[Implementation Guidelines]]

## Tags
#work-effort
#technical-requirements
#system-design
#documentation

---

> [!note] Navigation
> - [[Previous: Work Efforts Overview]]
> - [[Next: Implementation Details]]
"""

    def _get_router_template(self) -> str:
        return """---
title: "Router - {{we_id}}"
work-effort: "[[{{we_id}}]]"
type: router
status: active
created: {{date}}
tags:
  - chat-router
  - {{we_id}}
aliases:
  - {{we_id}} Chat Router
  - {{we_id}} Conversations
related:
  - "[[{{we_id}}]]"
  - "[[Chat Management]]"
recent-chats: []
archived-chats: []
---

# Chat History for {{we_id}}

## Active Conversations
- None yet
  <!-- Format: [[CH{{we_id[-4:]}}-{{date}}-001]] - Description -->

## Archived Conversations
- None yet

## Quick Links
- [[{{we_id}}|Back to Work Effort]]
- [[Chat Management|Chat Guidelines]]

## Tags
#chat-history #{{we_id}} #chat-router
"""

    def _get_chat_template(self) -> str:
        return """---
title: "Chat {{chat_id}} - {{we_id}}"
work-effort: "[[{{we_id}}]]"
type: chat
status: active
created: {{date}}
tags:
  - chat
  - {{we_id}}
  - {{chat_id}}
related:
  - "[[{{we_id}}]]"
  - "[[{{we_id}}/_router-{{we_id}}]]"
aliases:
  - {{chat_id}}
  - Chat {{chat_id}}
---

# Chat {{chat_id}} - {{we_id}}

## Context
[Add context here]

## Objectives
- [ ] First objective
- [ ] Second objective

## Chat History

### Initial Prompt
[Your initial prompt here]

### Response
[AI response here]

## Follow-up Actions
- [ ] First action item
- [ ] Second action item

## Related Chats
- None yet

## Tags
#chat #{{we_id}} #{{chat_id}}

---

> [!note] Navigation
> - [[{{we_id}}/_router-{{we_id}}|Back to Router]]
> - [[{{we_id}}|Back to Work Effort]]
"""

    def _create_readme(self) -> None:
        """Creates a README file explaining the templates."""
        readme_content = """# Work Effort Templates

## Templates
- `work_effort.md`: Main work effort document template
- `_router.md`: Chat router template
- `chat.md`: Individual chat template

## Variables
Templates use {{variable}} syntax for replacement:
- {{we_id}} - Work Effort ID
- {{date}} - Creation date
- {{chat_id}} - Chat session ID

## Usage
These templates are used by the work effort creation scripts to maintain consistent documentation structure.
"""
        with open(os.path.join(self.templates_dir, "README.md"), 'w') as f:
            f.write(readme_content)