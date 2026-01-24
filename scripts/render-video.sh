#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Render a final mp4 from clips and audio.

Usage:
  scripts/render-video.sh \
    --clip-list clips.txt \
    [--narration narration.mp3 | --narration-list narration_list.txt] \
    [--bgm bgm.mp3] [--bgm-volume 0.3] \
    [--audio mixed_audio.m4a] \
    [--srt subtitles.srt] \
    [--reencode] \
    --out output.mp4

Notes:
- clips.txt must be in ffmpeg concat format:
  file 'path/to/clip1.mp4'
  file 'path/to/clip2.mp4'
- If --audio is provided, narration/bgm are ignored.
- If clips have different codecs, use --reencode.
USAGE
}

clip_list=""
narration=""
narration_list=""
bgm=""
audio=""
srt=""
out=""
bgm_volume="0.3"
reencode="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clip-list)
      clip_list="$2"; shift 2 ;;
    --narration)
      narration="$2"; shift 2 ;;
    --narration-list)
      narration_list="$2"; shift 2 ;;
    --bgm)
      bgm="$2"; shift 2 ;;
    --bgm-volume)
      bgm_volume="$2"; shift 2 ;;
    --audio)
      audio="$2"; shift 2 ;;
    --srt)
      srt="$2"; shift 2 ;;
    --reencode)
      reencode="true"; shift 1 ;;
    --out)
      out="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage; exit 1 ;;
  esac
done

if [[ -z "$clip_list" || -z "$out" ]]; then
  echo "--clip-list and --out are required." >&2
  usage
  exit 1
fi

if [[ -n "$narration" && -n "$narration_list" ]]; then
  echo "Use either --narration or --narration-list, not both." >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found. Please install ffmpeg." >&2
  exit 1
fi

if [[ ! -f "$clip_list" ]]; then
  echo "clip list not found: $clip_list" >&2
  exit 1
fi

workdir="$(mktemp -d 2>/dev/null || mktemp -d -t render-video)"
trap 'rm -rf "$workdir"' EXIT

concat_video="$workdir/concat.mp4"

if [[ "$reencode" == "true" ]]; then
  ffmpeg -hide_banner -y -f concat -safe 0 -i "$clip_list" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    "$concat_video"
else
  ffmpeg -hide_banner -y -f concat -safe 0 -i "$clip_list" -c copy "$concat_video"
fi

mixed_audio="$workdir/mixed_audio.m4a"

if [[ -n "$audio" ]]; then
  ffmpeg -hide_banner -y -i "$audio" -c:a aac -b:a 192k "$mixed_audio"
else
  if [[ -n "$narration_list" ]]; then
    ffmpeg -hide_banner -y -f concat -safe 0 -i "$narration_list" -c copy "$workdir/narration_concat.mp3"
    narration="$workdir/narration_concat.mp3"
  fi

  if [[ -n "$narration" && -n "$bgm" ]]; then
    ffmpeg -hide_banner -y -i "$narration" -i "$bgm" \
      -filter_complex "[1:a]volume=${bgm_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]" \
      -map "[a]" -c:a aac -b:a 192k "$mixed_audio"
  elif [[ -n "$narration" ]]; then
    ffmpeg -hide_banner -y -i "$narration" -c:a aac -b:a 192k "$mixed_audio"
  elif [[ -n "$bgm" ]]; then
    ffmpeg -hide_banner -y -i "$bgm" -c:a aac -b:a 192k "$mixed_audio"
  fi
fi

video_with_audio="$workdir/video_with_audio.mp4"

if [[ -f "$mixed_audio" ]]; then
  ffmpeg -hide_banner -y -i "$concat_video" -i "$mixed_audio" -c:v copy -c:a aac -shortest "$video_with_audio"
else
  cp "$concat_video" "$video_with_audio"
fi

if [[ -n "$srt" ]]; then
  ffmpeg -hide_banner -y -i "$video_with_audio" \
    -vf "subtitles=${srt}:force_style='FontSize=24,PrimaryColour=&HFFFFFF'" \
    -c:v libx264 -preset medium -crf 18 -c:a aac "$out"
else
  cp "$video_with_audio" "$out"
fi

echo "Rendered: $out"
