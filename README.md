Terms
    Screen-New Terminal Window
    Ufw-Firewall that limits connectivity

Setup
    1.Installation of all covenants
        1.Install screen.
            apt install screen
        2.Set ufw
            apt install ufw
        3.Run openvpn-install.sh
            bash openvpn-install.sh
    Customize Total
        Start a separate screen
            screen -s title
            To exit ctrl + a D
            to enter screen -r title
        2.Start the checker
            cd checker(DO NOT CHANGE FOLDER NAME)
            python3 Checker.py
            P.s Everything above do in screenshot
