def show_help_manual() -> str:
    help_content = '''SUPPORTED COMMANDS:

    1-->  ! "sys command"
    2-->  ls
    3-->  pwd
    4-->  cd "path"
    5-->  mkdir "name"
    6-->  rename ./"old_name" ./"new_name"
    7-->  put "file name"
          put -r "dir name"
    8-->  get "file name"
          get -r "dir name"
    9-->  r
    10->  "command 1" && "command 2"
    11->  help
    12->  rm (just for files created by service account)
    13->  history

SAMPLES:

    1-->  Input:
                ! ls
          Output: (list of files and dirs for current dir on your PC)
                test1 my_dir large_file.txt cat.png
    2-->  Input:
                ls
          Output: (list of files and dirs for current dir on your Google Drive Account)
                All: 3 || Dirs: 1 || Files: 2
                dir -- test1
                file -- cat.png
                file -- document.docx
    3-->  Input:
                pwd
          Output: (full path to current dir on your Google Drive Account)
                /full/path/to/current/dir
    4-->  Input:
                cd ./MyDocs
          Output: (move to dir "MyDocs" from current dir ("./") on your Google Drive Account)
                (None)
    5-->  Input:
                mkdir new_dir
          Output: (create dir in current dir on your Google Drive Account)
                (None)
    6-->  Input:
                rename ./new_dir ./my_secret_info
          Output: (rename dir "new_dir" to "my_secret_info" on your Google Drive Account)
                (None)
    7-->  Input:
                put -r /home/user/need/my_project
          Output: (upload dir "my_project" from local PC into current dir on your Google Drive Account)
                START:
                Uploading "first.py": successfully
                Uploading "second.py": successfully
                ...
                Uploading "any.py": successfully
                :FINISHED
    8-->  Input:
                get ./my_table.xlsx
          Output: (download file "my_table.xlsx" from current dir on Google Drive Account into current local dir)
                Downloading "my_table.xlsx"
                Successfully
    9-->  Input:
                r
          Output: (update content of current dir (here: "MyDir") on Google Drive Account)
                MyDir's content was updated
    10->  Input:
                r && ls
          Output: (update content of current dir (here: "MyDir") AND list of files and dirs for current dir on Google Drive Account)
                MyDir's content was updated
                All: 3 || Dirs: 1 || Files: 2
                dir -- test1
                file -- cat.png
                file -- document.docx
    11->  Input:
                help
          Output:
                (this manual)
    12->  Input:
                rm ./junk_file.txt
          Output: (remove file "junk_file.txt" from current dir (if it created by service account) on your Google Drive Account)
                Remove "junk_file.txt": successfully
    13->  Input:
                history
          Output: (can contain last 50 commands, output it)
                ls
                cd ./MyDir && put ./best_code.cxx
                ...
                history
'''

    return help_content
