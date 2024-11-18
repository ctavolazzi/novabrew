#!/usr/bin/env python3

import os
import sys
import logging
from typing import Dict, Callable
from abc import ABC, abstractmethod
from work_effort_manager.managers.template import TemplateManager
from work_effort_manager.managers.work_effort import WorkEffortManager
from work_effort_manager.commands.base import Command

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class SetupTemplatesCommand(Command):
    def __init__(self, template_manager: TemplateManager):
        self.template_manager = template_manager

    def execute(self) -> bool:
        logger.info("\n=== Setting up Templates ===")
        return self.template_manager.create_templates()

    def description(self) -> str:
        return "Set up template files"

class CreateWorkEffortCommand(Command):
    def __init__(self, work_effort_manager: WorkEffortManager):
        self.work_effort_manager = work_effort_manager

    def execute(self) -> bool:
        logger.info("\n=== Creating Work Effort ===")
        we_id = self.work_effort_manager.generate_we_id()
        return self.work_effort_manager.create_we_structure(we_id)

    def description(self) -> str:
        return "Create new work effort"

class UnpackFacade:
    """Facade for all unpacking operations"""
    def __init__(self):
        self.template_manager = TemplateManager()
        self.work_effort_manager = WorkEffortManager()
        self.commands = {}

        # Initialize commands
        self.commands: Dict[str, Command] = {
            '1': SetupTemplatesCommand(self.template_manager),
            '2': CreateWorkEffortCommand(self.work_effort_manager),
            '3': self.create_combo_command()
        }

    def create_combo_command(self) -> Command:
        """Creates a command that runs all operations"""
        class ComboCommand(Command):
            def __init__(self, commands):
                self.commands = commands

            def execute(self) -> bool:
                logger.info("\n=== Running Full Setup ===")
                for cmd in self.commands.values():
                    if isinstance(cmd, ComboCommand):
                        continue
                    if not cmd.execute():
                        return False
                return True

            def description(self) -> str:
                return "Run all operations (templates + work effort)"

        return ComboCommand(self.commands)

    def show_menu(self) -> None:
        """Displays the operation menu"""
        logger.info("\n🚀 Work Effort Setup Menu 🚀")
        logger.info("=" * 30)
        for key, command in self.commands.items():
            logger.info(f"{key}. {command.description()}")
        logger.info("q. Quit")
        logger.info("=" * 30)

    def run(self) -> None:
        """Main execution loop"""
        while True:
            try:
                self.show_menu()
                choice = input("\nEnter your choice (1-3, q to quit): ").lower()

                if choice == 'q':
                    logger.info("\nGoodbye! 👋")
                    break

                if choice not in self.commands:
                    logger.error("Invalid choice! Please try again.")
                    continue

                command = self.commands[choice]
                if command.execute():
                    logger.info("✨ Operation completed successfully! ✨")
                else:
                    logger.error("❌ Operation failed! ❌")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                logger.info("\nOperation cancelled by user")
                break
            except Exception as e:
                logger.error(f"\nUnexpected error: {str(e)}")
                break

def main():
    """Entry point"""
    try:
        logger.info("🎉 Welcome to Work Effort Setup! 🎉")
        facade = UnpackFacade()
        facade.run()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()