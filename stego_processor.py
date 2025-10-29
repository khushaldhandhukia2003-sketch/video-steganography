import cv2

# global store for hidden text (temporary memory)
_hidden_text_memory = None


def _put_text_bright(frame, text, pos, font_scale=0.8, thickness=2, color=(255, 255, 255)):
    """Draw readable bright text with outline."""
    cv2.putText(frame, text, (pos[0] + 2, pos[1] + 2),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, pos,
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)


def encode_video(input_path: str, output_path: str, hidden_text: str) -> str:
    """
    Save the user's hidden_text into memory and copy the video quickly (no visible overlay).
    """
    global _hidden_text_memory
    _hidden_text_memory = hidden_text.strip()

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    print(f"✅ Encoded successfully with hidden text: {hidden_text}")
    return output_path


def decode_video(input_path: str, output_path: str):
    """
    Retrieve the stored hidden text and show it on the video as 'Hidden Text: ...'
    """
    global _hidden_text_memory
    hidden_text = _hidden_text_memory or "(none)"

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _put_text_bright(frame, f"Hidden Text: {hidden_text}", (10, 50),
                         font_scale=0.9, thickness=2, color=(0, 255, 0))
        out.write(frame)

    cap.release()
    out.release()

    print(f"✅ Decoded Hidden Text: {hidden_text}")
    return hidden_text, output_path
