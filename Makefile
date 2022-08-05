default: 
	cp -r /Applications/QQ.app/Contents/Frameworks/Hummer.framework .
	gcc -framework Hummer -F. -o remove_key remove_key.c
	install_name_tool -change @rpath/Hummer.framework/Versions/A/Hummer Hummer.framework/Versions/A/Hummer remove_key
	@echo ok

lldbinit:
	echo "\ncommand script import `pwd`/mozhu_cmd.py" >> ~/.lldbinit
	cat ~/.lldbinit

clean:
	sed -i '' '/.*mozhu_cmd.*/d' ~/.lldbinit
	rm -rf Hummer.framework
	rm -f remove_key