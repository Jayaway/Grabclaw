#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 测试脚本
运行方式：python test_api.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_schools():
    """测试学校列表接口"""
    print("\n=== 测试学校列表 ===")
    response = requests.get(f"{BASE_URL}/schools/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

def test_majors():
    """测试专业列表接口"""
    print("\n=== 测试专业列表 ===")
    response = requests.get(f"{BASE_URL}/majors/")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"专业数量: {len(data.get('data', []))}")
    if data.get('data'):
        print(f"第一个专业: {json.dumps(data['data'][0], ensure_ascii=False, indent=2)}")

def test_courses():
    """测试课程列表接口"""
    print("\n=== 测试课程列表 ===")
    response = requests.get(f"{BASE_URL}/courses/")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"课程数量: {len(data.get('data', []))}")
    if data.get('data'):
        print(f"第一门课程: {json.dumps(data['data'][0], ensure_ascii=False, indent=2)}")

def test_search():
    """测试搜索功能"""
    print("\n=== 测试搜索功能 ===")
    response = requests.get(f"{BASE_URL}/courses/?keyword=新闻")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"搜索结果数量: {len(data.get('data', []))}")

def test_statistics():
    """测试统计接口"""
    print("\n=== 测试统计接口 ===")
    response = requests.get(f"{BASE_URL}/courses/statistics/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

def test_submit_clue():
    """测试提交线索"""
    print("\n=== 测试提交线索 ===")
    clue_data = {
        "school_name": "中国传媒大学",
        "college_name": "新闻学院",
        "major_name": "新闻学",
        "course_name": "测试课程",
        "credits": 2.0,
        "reason": "测试提交",
        "submitter_contact": "test@example.com"
    }
    response = requests.post(
        f"{BASE_URL}/clues/",
        json=clue_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    print("🚀 开始测试 API...")
    print(f"📍 Base URL: {BASE_URL}")
    
    try:
        test_schools()
        test_majors()
        test_courses()
        test_search()
        test_statistics()
        test_submit_clue()
        
        print("\n✅ 所有测试完成！")
    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败！请确保服务器正在运行：")
        print("   cd /Users/vv/代码/微信小程序/course_death_backend")
        print("   source venv/bin/activate")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
