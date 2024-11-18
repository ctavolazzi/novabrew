#!/usr/bin/env python3

import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class WorkEffortManager:
    """Manages creation of work efforts"""
    def __init__(self, base_path=None):
        self.now = datetime.now()
        self.current_year = self.now.year
        self.current_date = self.now.strftime("%m%d")
        self.base_path = base_path or os.getcwd()  # Get current working directory
        logger.info(f"Work Effort Manager initialized with base_path: {self.base_path}")
        # Remove this line - it's from TemplateManager!
        # logger.info(f"Templates will be created in: {self.templates_dir}")


    def generate_we_id(self) -> str:
        """Generates a unique work effort ID."""
        seconds = self.now.second
        ms = int((self.now.timestamp() % 1) * 1000)
        return f"WE{seconds:02d}{ms:03d}-{self.current_date}-{self.current_year}"
    def create_we_structure(self, we_id: str) -> bool:
        """Creates the work effort folder structure and files."""
        we_path = os.path.join(self.base_path, we_id)

        try:
            logger.info(f"\nAttempting to create work effort structure:")
            logger.info(f"- Base path: {self.base_path}")
            logger.info(f"- Work effort path: {we_path}")

            # Create directories
            logger.info("Creating directories...")
            os.makedirs(we_path, exist_ok=True)
            os.makedirs(os.path.join(we_path, "chats"), exist_ok=True)

            # Create main WE file
            logger.info("Creating main file...")
            self._create_main_file(we_path, we_id)

            logger.info("Creating router file...")
            self._create_router_file(we_path, we_id)

            logger.info(f"Successfully created Work Effort: {we_id}")
            return True

        except Exception as e:
            logger.error(f"Error creating work effort: {str(e)}")
            return False

    def _create_main_file(self, we_path: str, we_id: str) -> None:
        """Creates the main work effort markdown file."""
        with open(os.path.join(we_path, f"{we_id}.md"), 'w') as f:
            f.write(self._get_main_file_content(we_id))

    def _create_router_file(self, we_path: str, we_id: str) -> None:
        """Creates the router markdown file."""
        with open(os.path.join(we_path, f"_router-{we_id}.md"), 'w') as f:
            f.write(self._get_router_file_content(we_id))

    def _get_main_file_content(self, we_id: str) -> str:
        return f"""---
title: "{we_id}"
created: {self.now.strftime("%Y-%m-%d")}
status: in-progress
type: documentation
aliases:
  - {we_id} Implementation
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
chat-router: "[[{we_id}/_router-{we_id}]]"
recent-chats: []
---

# {we_id}

## Initial Setup

> [!question] Initial Requirements
> **Preview:** [Brief description]
>
> > [!abstract]- Full Content (Click to expand)
> > ```markdown
> > [Detailed content]
> > ```

## Technical Requirements Development

### {we_id} - Iteration 1
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

    def _get_router_file_content(self, we_id: str) -> str:
        return f"""---
title: "Router - {we_id}"
work-effort: "[[{we_id}]]"
type: router
status: active
created: {self.now.strftime("%Y-%m-%d")}
tags:
  - chat-router
  - {we_id}
aliases:
  - {we_id} Chat Router
  - {we_id} Conversations
related:
  - "[[{we_id}]]"
  - "[[Chat Management]]"
recent-chats: []
archived-chats: []
---

# Chat History for {we_id}

## Active Conversations
- None yet
  <!-- Format: [[CH{we_id[-4:]}-{self.current_date}-{self.current_year}-001]] - Description -->

## Archived Conversations
- None yet

## Quick Links
- [[{we_id}|Back to Work Effort]]
- [[Chat Management|Chat Guidelines]]

## Tags
#chat-history #{we_id} #chat-router
"""