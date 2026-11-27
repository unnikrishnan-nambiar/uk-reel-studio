import subprocess
D='/home/claude/uk-reel-studio/jobs/privacy_v1';O='/home/claude/uk-reel-studio/output';U='/mnt/user-data/outputs'
CV='scale=in_color_matrix=bt601:in_range=tv,format=gbrp16le,scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le'
HV=['-c:v','libx265','-pix_fmt','yuv420p10le','-tag:v','hvc1','-color_primaries','bt2020','-color_trc','arib-std-b67','-colorspace','bt2020nc','-color_range','tv']
XP='colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:hdr10=0:log-level=error'
fc='[1:a]volume=0.32[sx];[0:a][sx]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aa];[0:v]fps=60,setsar=1,'+CV+'[vv]'
m=f'{O}/privacy-hook1.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/body.mp4','-i',f'{D}/sfx.wav','-filter_complex',fc,'-map','[vv]','-map','[aa]',*HV,'-preset','fast','-crf','17','-x265-params',XP+':pools=2:frame-threads=1','-r','60','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',m],check=True)
subprocess.run(['cp',m,f'{U}/privacy-hook1.mp4'])
print('done',flush=True)
