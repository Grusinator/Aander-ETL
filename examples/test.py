from progress import progress, startProgress, endProgress

startProgress("test")
for i in range(100):
    progress(i)

endProgress()

