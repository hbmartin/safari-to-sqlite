tell application "Safari"
	set sep to "150r2M72e7D6Lb7Z9u1g4BSQBonv6U21W1fmX8B1TXR8XXqB2wTgQzqwoB06144d"
	set linkList to ""
	
	repeat with w in windows
		set windowId to id of w
		if windowId < 0 then
			exit repeat
		end if
		
		set tabCount to count of tabs of w
		repeat with t from tabCount to 1 by -1
			set theTab to tab t of w
			try
				set linkList to linkList & (URL of theTab) & "
"
				set linkList to linkList & (name of theTab) & "
"
				set linkList to linkList & (windowId as string) & "
"
				set linkList to linkList & (t as string) & "
"
				set linkList to linkList & (text of theTab) & "
"
				set linkList to linkList & sep & "
"
			on error errMsg
				log errMsg
				exit repeat
			end try
		end repeat
	end repeat

	log linkList
end tell
