"""
04_vision_demo.py
Claude 视觉能力（Vision）示例

演示如何使用 Claude 分析图像
"""
import os
import base64
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()


def analyze_image_from_url(image_url: str, question: str) -> str:
    """
    分析网络图片

    Args:
        image_url: 图片 URL
        question: 关于图片的问题
    """
    import httpx

    # 下载图片并转为 base64
    image_data = base64.standard_b64encode(
        httpx.get(image_url).content
    ).decode("utf-8")

    # 根据 URL 推断图片类型
    if image_url.lower().endswith(".png"):
        media_type = "image/png"
    elif image_url.lower().endswith(".gif"):
        media_type = "image/gif"
    elif image_url.lower().endswith(".webp"):
        media_type = "image/webp"
    else:
        media_type = "image/jpeg"

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text


def analyze_image_from_file(file_path: str, question: str) -> str:
    """
    分析本地图片

    Args:
        file_path: 图片文件路径
        question: 关于图片的问题
    """
    # 读取文件并转为 base64
    with open(file_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # 根据文件扩展名确定媒体类型
    ext = file_path.lower().split(".")[-1]
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    media_type = media_types.get(ext, "image/jpeg")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text


def analyze_multiple_images(images: list, question: str) -> str:
    """
    同时分析多张图片

    Args:
        images: 图片列表，每项为 {"type": "url"|"file", "path": "..."}
        question: 关于图片的问题
    """
    import httpx

    content = []

    for img in images:
        if img["type"] == "url":
            image_data = base64.standard_b64encode(
                httpx.get(img["path"]).content
            ).decode("utf-8")
            media_type = "image/jpeg"
        else:  # file
            with open(img["path"], "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")
            ext = img["path"].lower().split(".")[-1]
            media_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_data
            }
        })

    # 添加问题文本
    content.append({
        "type": "text",
        "text": question
    })

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{"role": "user", "content": content}]
    )

    return message.content[0].text


def demo_vision_capabilities():
    """展示 Vision 能力说明"""
    print("=" * 60)
    print("【Claude Vision 能力说明】")
    print("=" * 60)

    capabilities = """
    Claude Vision 支持的任务：

    📷 图像理解
    ├── 物体识别：识别图片中的物体、人物、场景
    ├── 文字识别（OCR）：提取图片中的文字
    ├── 图表分析：解读数据图表、流程图
    └── 界面分析：分析 UI 设计、网页截图

    📊 支持的图片格式
    ├── JPEG / JPG
    ├── PNG
    ├── GIF
    └── WebP

    ⚠️ 限制
    ├── 单张图片最大 20MB
    ├── 单次请求最多 20 张图片
    └── 图片越大，消耗 Token 越多

    💡 最佳实践
    ├── 图片清晰度：确保关键内容清晰可见
    ├── 问题具体化：具体说明需要分析什么
    └── 合理压缩：大图片适当压缩以节省成本
    """
    print(capabilities)


def demo_ocr():
    """OCR 文字识别示例（代码展示）"""
    print("\n" + "=" * 60)
    print("【OCR 文字识别示例代码】")
    print("=" * 60)

    code = '''
def extract_text_from_image(image_path: str) -> str:
    """从图片中提取文字（OCR）"""
    import anthropic
    import base64

    client = anthropic.Anthropic()

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """请仔细识别并提取图片中的所有文字内容。
要求：
1. 保持原文的格式和结构
2. 如果有表格，用 Markdown 表格格式输出
3. 如果文字不清晰，标注 [不清晰]
4. 只输出识别到的文字，不要添加解释"""
                    }
                ]
            }
        ]
    )

    return message.content[0].text

# 使用示例
# text = extract_text_from_image("screenshot.png")
# print(text)
    '''
    print(code)


if __name__ == "__main__":
    demo_vision_capabilities()
    demo_ocr()

    # 实际调用示例（需要有网络图片）
    print("\n" + "=" * 60)
    print("【实际调用演示】")
    print("=" * 60)

    # 使用一个公开的示例图片
    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/300px-PNG_transparency_demonstration_1.png"

    try:
        print(f"\n分析图片: {test_url[:50]}...")
        result = analyze_image_from_url(test_url, "请描述这张图片的内容，包括你看到的所有元素。")
        print(f"\n分析结果:\n{result}")
    except Exception as e:
        print(f"演示跳过（需要网络）: {e}")
