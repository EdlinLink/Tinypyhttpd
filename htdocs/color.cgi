#!/usr/bin/python


color = raw_input()

body = '''
<head>
<title>%s</title>
</head>
<body bgcolor="%s">
<h1>This is %s</h1>
</body>
</html>
''' %(color, color, color)

if __name__ == "__main__":
	print "\r\n".join(body.split("\n"))
