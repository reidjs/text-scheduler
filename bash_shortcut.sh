stxt(){
    run_schedule=${1:-0}
    cd /your/path/to/cloned/repo
    python gui.py
    if [ "$run_schedule" -eq 1 ]; then
        python send_scheduled_messages.py
    fi
    cd $OLDPWD
}