# bchud


Game Instance 
- Move all the estimation functions to the game instance
  - level file is purely read the level file
  - log files is purely read the log files
- Adjust the next update time to be based on the gametime (6000) and not the mtime
- Change the estimation to be based on current session start time or mtime depending on what is latest

- Optimize each function call timer and make the read functions every other 2 or 3 seconds or based on predicted update time
- If place side window in another works space and make 0 be the default - only update as needed - 
- use one time call for the whole status windows updates (estimations)