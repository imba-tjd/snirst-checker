// go:build windows
package main

import (
	"crypto/tls"
	"errors"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"syscall"
	"time"
)

func main() {
	// sn, dfip := parseCmd()
	// sn, dfip := parseCmd2(), DFIPDefault
	sn, dfip := "bbc.com", DFIPDefault

	ok, err := Check(sn, dfip)
	if ok {
		fmt.Println("ok")
		return
	} else {
		if os.IsTimeout(err) {
			fmt.Println("timeout")
		} else if errors.Is(err, syscall.WSAECONNRESET) {
			// } else if syscall.WSAECONNRESET == err.(*net.OpError).Err.(*os.SyscallError).Err.(syscall.Errno) {
			fmt.Println("rst")
		} else {
			log.Fatalln(err)
		}
	}
}

const Timeout = 5
const DFIPDefault = "104.131.212.184"

var dialer = &net.Dialer{Timeout: 5 * time.Second}

func Check(servername, ip string) (bool, error) {
	conn, err := tls.DialWithDialer(dialer, "tcp", ip+":443", &tls.Config{ServerName: servername})
	if err != nil {
		return false, err
	}
	conn.Close()
	return true, nil
}

func parseCmd() (sn, dfip string) {
	flag.StringVar(&sn, "servername", "", "The host to be checked")
	flag.StringVar(&dfip, "dfip", DFIPDefault, "The domain front IP")
	flag.Parse()

	if sn == "" {
		flag.Usage()
		log.SetFlags(0)
		log.Fatal()
	}

	return
}

func parseCmd2() string {
	if len(os.Args) != 2 {
		log.SetFlags(0)
		log.Fatalln("invalid args")
	}
	return os.Args[1]
}
