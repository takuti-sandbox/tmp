  RE_IP_BLOCK = /\d{,2}|1\d{2}|2[0-4]\d|25[0-5]/
  RE_IP = /\A#{RE_IP_BLOCK}\.#{RE_IP_BLOCK}\.#{RE_IP_BLOCK}\.#{RE_IP_BLOCK}\z/

  p '192.168.0.1' =~ RE_IP
  p '255.255.255.255' =~ RE_IP
  p '255.255.255.2555' =~ RE_IP
  p '255.255.255.256' =~ RE_IP
