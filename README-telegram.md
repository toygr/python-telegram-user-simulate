# Create multiple telegram profiles in ubuntu
```
mkdir -p ~/.local/share/TelegramDesktop/Account1
mkdir -p ~/.local/share/TelegramDesktop/Account2
```
> Repeat for as many accounts as needed
```
touch ~/.local/share/applications/telegramdesktop-account1.desktop
touch ~/.local/share/applications/telegramdesktop-account2.desktop
```
> Repeat for as many accounts as needed
```
[Desktop Entry]
Name=Telegram Account1
Comment=Telegram messaging app - Account1
TryExec=/home/ubuntu/Apps/tsetup.5.10.4/Telegram/Telegram
Exec=/home/ubuntu/Apps/tsetup.5.10.4/Telegram/Telegram -workdir /home/ubuntu/.local/share/TelegramDesktop/Account1 -- %u
Icon=telegram
Terminal=false
StartupWMClass=TelegramDesktop
Type=Application
Categories=Chat;Network;InstantMessaging;Qt;
MimeType=x-scheme-handler/tg;x-scheme-handler/tonsite;
Keywords=tg;chat;im;messaging;messenger;sms;tdesktop;
Actions=quit;
DBusActivatable=true
SingleMainWindow=true
X-GNOME-UsesNotifications=true
X-GNOME-SingleWindow=true

[Desktop Action quit]
Exec=/home/ubuntu/Apps/tsetup.5.10.4/Telegram/Telegram -quit
Name=Quit Telegram
Icon=application-exit
```
```
chmod +x ~/.local/share/applications/telegramdesktop-account1.desktop
chmod +x ~/.local/share/applications/telegramdesktop-account2.desktop
```
> Repeat for all created .desktop files
