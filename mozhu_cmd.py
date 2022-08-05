#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2022/08/04, 21:45
"""

import lldb, os


def breakpointHandler(frame, bp_loc, dict):
    thread = frame.GetThread()
    process = thread.GetProcess()
    debugger = process.GetTarget().GetDebugger()
    function_name = frame.GetFunctionName()
    err = lldb.SBError()
    print("[+] Handler : %s" % function_name)

    try:
        if function_name in [
            "sqlite3_open",
            "sqlite3_open16",
            "sqlite3_open_v2",
        ]:
            # $arg1 - rdi
            membuff = process.ReadCStringFromMemory(
                int(frame.FindRegister("rdi").value, 16), 256, err
            )
            if err.Success() and len(membuff) > 0:
                print("\033[0;37;41m[+] Database: \033[0;37;44m[%s]\033[0m" % membuff)
        elif function_name in ["sqlite3_key", "sqlite3_rekey"]:
            # $arg2 - rsi
            addr = int(frame.FindRegister("rsi").value, 16)
            try:
                membuff = process.ReadCStringFromMemory(addr, 20, err)
                if err.Success() and len(membuff) > 0:
                    print(
                        "\033[0;37;41m[+] SqliteFile: \033[0;37;44m[%s]\033[0m"
                        % membuff
                    )
            except SystemError as e:
                print("[-] %s" % e)
                membuff = process.ReadMemory(addr, 16, err)
                if err.Success() and len(membuff) > 0:
                    print(
                        "\033[0;37;41m[+] SqliteKey: \033[0;37;44m[%s]\033[0m" % membuff
                    )
    except SystemError as e:
        print("[-] %s" % e)
    finally:
        process.Continue()


def mozhu_find_qq_sqlite_key(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    if not target:
        print("[-] error: no target available. please add a target to lldb.")
        return
    module_found = False
    for i in target.modules:
        if "Hummer" in "[~] %s" % i:
            print("[+] Found %s" % i)
            module_found = True
            break
    if not module_found:
        print("[-] Not Found Hummer.framework")
        return

    funcs = [
        "sqlite3_key",
        "sqlite3_rekey",
        "sqlite3_open",
        "sqlite3_open16",
        "sqlite3_open_v2",
    ]
    debugger.SetAsync(False)
    for func in funcs:
        bp = target.BreakpointCreateByName(func)
        if not bp.IsValid() or bp.num_locations == 0:
            result.AppendWarning("Breakpoint isn't valid or hasn't found any hits")
        else:
            result.AppendMessage("{}".format(bp))
        bp.SetScriptCallbackFunction("mozhu_cmd.breakpointHandler")

    target.LaunchSimple(None, None, os.getcwd())


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
        "command script add -f mozhu_cmd.mozhu_find_qq_sqlite_key mozhu_fqsk"
    )
    print('The "mozhu_fqsk" python command has been installed and is ready for use.')
