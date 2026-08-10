@echo off

cd /d "%~dp0.."

echo ========================================
echo   AksaraNusantara - QuizTab Test Suite
echo ========================================
echo.

python tests\test_quiz_tab.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_ui.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_visual.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_feedback.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_controls.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_progress.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_progress_ui.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_statistics.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_statistics_ui.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_completion.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_restart.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_session_isolation.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_answer_guard.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_difficulty_guard.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_control_lifecycle.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_signals.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_integration.py
if errorlevel 1 goto :FAILED

python tests\test_quiz_tab_answer_buttons_ui.py
if errorlevel 1 goto :FAILED

echo.
echo ========================================
echo   ALL QUIZTAB TESTS PASSED
echo ========================================
exit /b 0

:FAILED
echo.
echo ========================================
echo   QUIZTAB TEST SUITE FAILED
echo ========================================
exit /b 1