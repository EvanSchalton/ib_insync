# Refactor One-Per-File

Refactor a Python file into a directory with one class/function per file, following project development patterns.

## Algorithm

This command implements the standard refactoring pattern used in this project:

1. **Create directory** with same name as the file (minus .py extension)
2. **Move original file** into directory as `__init__.py`
3. **Extract classes/functions** one by one into separate files
4. **Update __init__.py** to import each extracted item
5. **Final __init__.py** should only contain imports and `__all__` declaration

## Usage

```bash
/refactor-one-per-file <file_path>
```

**Example:**
```bash
/refactor-one-per-file /workspaces/Tmux-Orchestrator/tmux_orchestrator/utils/tmux/exceptions.py
```

## Process Steps

### Step 1: Directory Setup
- Create directory: `exceptions/` (from `exceptions.py`)
- Move file: `exceptions.py` → `exceptions/__init__.py`
- Verify imports still work

### Step 2: Extract Classes/Functions
For each class/function in the original file:
- Create new file: `exceptions/tmux_error.py` (for `TmuxError` class)
- Move class definition with all methods and docstrings
- Add necessary imports to new file
- Add import to `exceptions/__init__.py`

### Step 3: Final Cleanup
- `__init__.py` should only contain:
  ```python
  """Module description."""

  from .tmux_error import TmuxError
  from .tmux_session_error import TmuxSessionError
  # ... more imports

  __all__ = [
      'TmuxError',
      'TmuxSessionError',
      # ... all exported items
  ]
  ```

## Benefits

- **Single Responsibility**: Each file has one clear purpose
- **Easy Navigation**: Developers can quickly find specific code
- **Better Maintenance**: Smaller files are easier to understand and modify
- **Clean Imports**: Centralized import management with `__all__`

## References

- See `/workspaces/Tmux-Orchestrator/.claude/commands/development-patterns.md` for full development patterns
- This follows the "one function per file" principle established in the project
- Maintains backward compatibility during refactoring

## Implementation Notes

- Always test imports after each step
- Preserve all docstrings and type hints
- Maintain existing functionality - refactoring should be transparent to users
- Follow existing naming conventions for new files
