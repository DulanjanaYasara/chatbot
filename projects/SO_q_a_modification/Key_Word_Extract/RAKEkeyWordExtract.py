from commons import rake

# EXAMPLE ONE - SIMPLE
stoppath = "../../rake/SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath)

# 2. run on RAKE on a given text
text = """Two things might be happening.

IE is masking an HTTP error response with its friendly errors. 
Since this is a remote server, iptables could be running on the server, or there is another firewall in the way blocking that port. 

To diagnose, I would start by disabling friendly error messages in IE, or using a different browser that doesn't do 
this. Instructions on how to disable it here: http://technet.microsoft.com/en-us/library/cc778248(v=ws.10).aspx Next, 
if that doesn't resolve it, I would try running curl/wget on the server, and requesting the displayed URL. curl can 
be run with curl example.com and wget wget -qO- example.com, both will displayed the returned data (if any) on the 
terminal. If one returns a command not found, try the other. If that doesn't work, something is going on with your 
server. If it's returning something that looks like an error (e.g. a sever generated error page), I'd look into that 
too at this step. If you appear to have connectivity issues, you can see if there's any iptables rules in place by 
running iptables -L on the server. A DROP all under Chain INPUT would cause this. You can read more about iptables 
here, and how to set it up for your needs here: https://help.ubuntu.com/community/IptablesHowTo (Even if you're not 
using ubuntu, this will still work for you, look in the "Allowing Incoming Traffic on Specific Ports" section, 
there's an example there you would need to adopt slightly for the non-standard port the server is running on). If 
there's an external firewall preventing access, you would need to talk with whoever is managing the sever. """

keywords = rake_object.run(text)

# 3. print results
print("Keywords:", keywords)
