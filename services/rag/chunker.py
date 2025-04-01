class SlidingWindowChunking:
    """
    A class used to perform sliding window chunking on text data.
    This class provides methods to split text into chunks of a specified window size
    with a given step size. It also summarizes with an LLM if possible and filters the markdown
    """

    def __init__(self, window_size=135, step=35):
        self.window_size = window_size
        self.step = step
    
    def chunk(self, text, window_size=0,step=0) -> list[str]:
        window_size = window_size or self.window_size
        step = step or self.step

        words = text.split(" ")
        chunks = []
        for i in range(0, len(words) - window_size + 1, step):
            chosen = words[i:i + window_size]
            if chosen:
                chunks.append(' '.join(chosen))
        if not chunks:
            chunks = [text]
        return chunks
    